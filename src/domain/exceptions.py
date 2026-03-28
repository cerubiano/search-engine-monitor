class DomainError(Exception):
    """Base exception for all domain errors."""


class SnapshotError(DomainError):
    """Raised when snapshot processing fails."""


class CoverageAnalysisError(DomainError):
    """Raised when coverage analysis cannot be completed."""


class AnomalyDetectionError(DomainError):
    """Raised when anomaly detection cannot be completed."""


class AdapterError(Exception):
    """Raised when an external API call fails."""


class RepositoryError(Exception):
    """Raised when a storage operation fails."""