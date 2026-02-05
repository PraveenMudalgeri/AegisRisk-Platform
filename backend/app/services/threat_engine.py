import json
import os
from typing import List, Dict
from ..models.enums import AssetType, STRIDECategory

class ThreatEngine:
    def __init__(self):
        self.threats_db = self._load_threats()
    
    def _load_threats(self) -> List[Dict]:
        try:
            # Assuming file is at app/data/stride_threats.json
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            file_path = os.path.join(base_dir, "data", "stride_threats.json")
            
            with open(file_path, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading threats DB: {e}")
            return []

    def enumerate_threats(self, asset_type: AssetType) -> List[Dict]:
        """
        Returns a list of potential threats based on the asset type.
        This is a simplified rule engine.
        """
        relevant_categories = []
        
        if asset_type == AssetType.DATA:
            relevant_categories = [
                STRIDECategory.TAMPERING, 
                STRIDECategory.INFORMATION_DISCLOSURE, 
                STRIDECategory.REPUDIATION
            ]
        elif asset_type == AssetType.SOFTWARE:
            relevant_categories = [
                STRIDECategory.SPOOFING,
                STRIDECategory.TAMPERING,
                STRIDECategory.ELEVATION_OF_PRIVILEGE,
                STRIDECategory.DENIAL_OF_SERVICE
            ]
        elif asset_type == AssetType.HARDWARE:
            relevant_categories = [
                STRIDECategory.DENIAL_OF_SERVICE,
                STRIDECategory.TAMPERING
            ]
        elif asset_type == AssetType.PEOPLE:
             relevant_categories = [
                STRIDECategory.SPOOFING, # Social engineering
                STRIDECategory.INFORMATION_DISCLOSURE
             ]
        else:
            # Default to all for unknown or other types
            return self.threats_db

        return [t for t in self.threats_db if t["category"] in relevant_categories]

threat_engine = ThreatEngine()
