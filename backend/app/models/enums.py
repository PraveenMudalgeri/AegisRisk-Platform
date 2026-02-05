from enum import Enum

class RiskSeverity(str, Enum):
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    INFORMATIONAL = "Informational"

class RiskLikelihood(str, Enum):
    RARE = "Rare"
    UNLIKELY = "Unlikely"
    POSSIBLE = "Possible"
    LIKELY = "Likely"
    ALMOST_CERTAIN = "Almost Certain"

class AssetType(str, Enum):
    HARDWARE = "Hardware"
    SOFTWARE = "Software"
    DATA = "Data"
    PEOPLE = "People"
    PROCESS = "Process"
    FACILITY = "Facility"

class STRIDECategory(str, Enum):
    SPOOFING = "Spoofing"
    TAMPERING = "Tampering"
    REPUDIATION = "Repudiation"
    INFORMATION_DISCLOSURE = "Information Disclosure"
    DENIAL_OF_SERVICE = "Denial of Service"
    ELEVATION_OF_PRIVILEGE = "Elevation of Privilege"

class ImplementationStatus(str, Enum):
    IMPLEMENTED = "Implemented"
    NOT_IMPLEMENTED = "Not Implemented"
    PLANNED = "Planned"
    PARTIALLY_IMPLEMENTED = "Partially Implemented"
    NOT_APPLICABLE = "Not Applicable"

class Framework(str, Enum):
    ISO27001 = "ISO27001"
    NIST_800_53 = "NIST 800-53"
