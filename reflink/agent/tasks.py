"""
Reflink agent tasks.

This is intended to be the primary entry-point into the processing component of
the service.
"""

from reflink import logging
from reflink.config import VERSION
from reflink.services import ExtractionEvents, DataStore
from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task
def create_failed_event(task_id: str, document_id: str) -> dict:
    """Commemorate extraction failure."""
    try:
        extractions = ExtractionEvents().session
        data = extractions.create(document_id, state=extractions.FAILED)
    except IOError as e:
        msg = 'Failed to store failed state for %s: %s' % (document_id, e)
        logger.error(msg)
        raise RuntimeError(msg)
    return data


@shared_task
def create_success_event(extraction_id: str, document_id: str) -> dict:
    """Commemorate extraction success."""
    try:
        extractions = ExtractionEvents().session
        data = extractions.create(document_id, state=extractions.COMPLETED,
                                  extraction=extraction_id)
    except IOError as e:
        msg = 'Failed to store success state for %s: %s' % (document_id, e)
        logger.error(msg)
        raise RuntimeError(msg)
    return data


@shared_task
def store(document_id: str, metadata: list, version: str=VERSION) -> str:
    """
    Deposit extracted references in the datastore.

    Parameters
    ----------
    document_id : str
    metadata : str

    Returns
    -------
    str
        Unique identifier for this extraction.
    """
    logger.info('Storing metadata for %s' % document_id)
    datastore = DataStore()

    try:
        # Should return the data with reference hashes inserted.
        extraction, metadata = datastore.session.create(document_id, metadata,
                                                        version)
    except IOError as e:    # Separating this out in case we want to retry.
        msg = 'Could not store metadata for document %s: %s' % (document_id, e)
        logger.error(msg)
        raise RuntimeError(msg) from e
    except Exception as e:
        msg = 'Could not store metadata for document %s: %s' % (document_id, e)
        logger.error(msg)
        raise RuntimeError(msg) from e
    logger.info('Stored metadata for %s with extraction %s' %
                (document_id, extraction))
    return extraction
