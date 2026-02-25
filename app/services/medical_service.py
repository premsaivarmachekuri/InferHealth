import pandas as pd
import chromadb
import os
from math import radians, cos, sin, sqrt, atan2
from app.core.config import settings
from app.utils.geo import get_coordinates

class MedicalService:
    def __init__(self):
        self.chroma_client = chromadb.PersistentClient(path=settings.CHROMA_DB_PATH)
        self.collection = self.chroma_client.get_or_create_collection(name="medical_q_n_a")
        self._initialize_data()

    def _initialize_data(self):
        # Hospital Data
        hosp_path = os.path.join(settings.DATA_PATH, "hospitals.csv")
        if os.path.exists(hosp_path):
            self.df_hospital = pd.read_csv(hosp_path)
        else:
            print(f"Warning: Hospital data not found at {hosp_path}")
            self.df_hospital = pd.DataFrame()

        # QA Data - In production, this would be pre-indexed
        qa_path = os.path.join(settings.DATA_PATH, "train.csv")
        if os.path.exists(qa_path) and self.collection.count() == 0:
            df_qa = pd.read_csv(qa_path).sample(500, random_state=0).reset_index(drop=True)
            df_qa["combined_text"] = (
                "Question: " + df_qa["Question"].astype(str) + ". " +
                "Answer: " + df_qa["Answer"].astype(str) + ". "  +
                ": " + df_qa["qtype"].astype(str) + ". "  
            )
            self.collection.add(
                documents=df_qa['combined_text'].tolist(),
                metadatas=df_qa.to_dict(orient="records"),
                ids=df_qa.index.astype(str).tolist(),
            )

    def retrieve_context(self, query: str):
        """Retrieves relevant medical Q&A context."""
        results = self.collection.query(query_texts=[query], n_results=3)
        context = "\n".join(results["documents"][0])
        return {"context": context, "source": "Medical Q&A Collection"}

    def search_nearest_hospital(self, user_location: str, specialty: str = None, top_n: int = 3):
        """Finds nearest hospitals based on geolocation."""
        user_coords = get_coordinates(user_location)
        if not user_coords:
            return {"error": "Could not get coordinates"}
        
        user_lat, user_lon = user_coords

        def haversine(lat1, lon1, lat2, lon2):
            lat1, lon1, lat2, lon2 = map(radians, [float(lat1), float(lon1), float(lat2), float(lon2)])
            dlon = lon2 - lon1
            dlat = lat2 - lat1
            a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
            c = 2 * atan2(sqrt(a), sqrt(1-a))
            return 6371 * c  # km

        filtered_df = self.df_hospital.copy()
        if specialty:
            filtered_df = filtered_df[filtered_df['TYPE'].str.contains(specialty, case=False, na=False)]

        filtered_df['distance_km'] = filtered_df.apply(
            lambda row: haversine(user_lat, user_lon, row['LATITUDE'], row['LONGITUDE']), axis=1
        )

        nearest = filtered_df.sort_values('distance_km').head(top_n)
        nearest["distance_km"] = nearest["distance_km"].round(2)
        results = nearest[['NAME','ADDRESS','CITY','STATE','TYPE','BEDS','WEBSITE','distance_km']].to_dict(orient='records')
        return {"context": results, "source": "Hospital Search"}

medical_service = MedicalService()
