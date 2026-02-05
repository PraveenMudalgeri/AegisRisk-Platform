from typing import List, Dict
from ..models.enums import STRIDECategory

class ThreatControlMapper:
    def recommend_controls(self, stride_category: STRIDECategory) -> List[str]:
        """
        Suggests relevant ISO 27001 or NIST controls based on the STRIDE category.
        """
        recommendations = []
        
        if stride_category == STRIDECategory.SPOOFING:
            recommendations.extend([
                "ISO27001-A.9.2.1: User registration and de-registration",
                "ISO27001-A.9.4.1: Information access restriction",
                "NIST-IA-2: Identification and Authentication"
            ])
        elif stride_category == STRIDECategory.TAMPERING:
            recommendations.extend([
                "ISO27001-A.10.1.1: Policy on value of cryptographic controls",
                "ISO27001-A.14.1.2: Securing application services on public networks",
                "NIST-SI-7: Software, Firmware, and Information Integrity"
            ])
        elif stride_category == STRIDECategory.REPUDIATION:
            recommendations.extend([
                "ISO27001-A.12.4.1: Event logging",
                "ISO27001-A.12.4.2: Protection of log information",
                "NIST-AU-2: Audit Events"
            ])
        elif stride_category == STRIDECategory.INFORMATION_DISCLOSURE:
            recommendations.extend([
                "ISO27001-A.8.2.1: Classification of information",
                "ISO27001-A.13.2.1: Information transfer policies and procedures",
                "NIST-SC-8: Transmission Confidentiality and Integrity"
            ])
        elif stride_category == STRIDECategory.DENIAL_OF_SERVICE:
            recommendations.extend([
                "ISO27001-A.17.1.1: Planning information security continuity",
                "ISO27001-A.12.1.3: Capacity management",
                "NIST-SC-5: Denial of Service Protection"
            ])
        elif stride_category == STRIDECategory.ELEVATION_OF_PRIVILEGE:
            recommendations.extend([
                "ISO27001-A.9.2.3: Management of privileged access rights",
                "NIST-AC-6: Least Privilege"
            ])
            
        return recommendations

threat_control_mapper = ThreatControlMapper()
