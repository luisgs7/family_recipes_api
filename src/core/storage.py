import os
from django.conf import settings
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from minio import Minio
from minio.error import S3Error
import logging

logger = logging.getLogger(__name__)


@deconstructible
class MinIOStorage(Storage):
    """Custom storage class for MinIO"""

    def __init__(self, bucket_name=None):
        self.bucket_name = bucket_name or settings.MINIO_BUCKET_NAME
        self._client = None
        self._ensure_bucket_exists()

    @property
    def client(self):
        """Lazy initialization of MinIO client"""
        if self._client is None:
            self._client = Minio(
                settings.MINIO_ENDPOINT,
                access_key=settings.MINIO_ACCESS_KEY,
                secret_key=settings.MINIO_SECRET_KEY,
                secure=settings.MINIO_SECURE,
            )
        return self._client

    def _ensure_bucket_exists(self):
        """Ensure the bucket exists, create if it doesn't"""
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
                logger.info(f"Created bucket: {self.bucket_name}")
        except Exception as e:
            logger.warning(f"MinIO not available during initialization: {e}")
            # Don't fail during Django startup

    def _open(self, name, mode="rb"):
        """Open file for reading"""
        try:
            response = self.client.get_object(self.bucket_name, name)
            return response
        except S3Error as e:
            logger.error(f"Error opening file {name}: {e}")
            raise

    def _save(self, name, content):
        """Save file to MinIO"""
        try:
            # Reset file pointer to beginning
            content.seek(0)

            # Get file size
            content.seek(0, 2)  # Seek to end
            file_size = content.tell()
            content.seek(0)  # Reset to beginning

            # Upload file
            self.client.put_object(
                self.bucket_name,
                name,
                content,
                file_size,
                content_type=self._get_content_type(name),
            )
            logger.info(f"Successfully uploaded {name} to MinIO")
            return name
        except S3Error as e:
            logger.error(f"Error saving file {name}: {e}")
            raise

    def delete(self, name):
        """Delete file from MinIO"""
        try:
            self.client.remove_object(self.bucket_name, name)
            logger.info(f"Successfully deleted {name} from MinIO")
        except S3Error as e:
            logger.error(f"Error deleting file {name}: {e}")
            raise

    def exists(self, name):
        """Check if file exists in MinIO"""
        try:
            self.client.stat_object(self.bucket_name, name)
            return True
        except S3Error:
            return False

    def listdir(self, path):
        """List files in directory"""
        try:
            objects = self.client.list_objects(self.bucket_name, prefix=path, recursive=True)
            files = []
            dirs = set()

            for obj in objects:
                relative_path = obj.object_name[len(path) :].lstrip("/")  # noqa: E203
                if "/" in relative_path:
                    dirs.add(relative_path.split("/")[0])
                else:
                    files.append(relative_path)

            return list(dirs), files
        except S3Error as e:
            logger.error(f"Error listing directory {path}: {e}")
            return [], []

    def size(self, name):
        """Get file size"""
        try:
            stat = self.client.stat_object(self.bucket_name, name)
            return stat.size
        except S3Error as e:
            logger.error(f"Error getting size of {name}: {e}")
            return 0

    def url(self, name):
        """Get file URL"""
        return f"{settings.MEDIA_URL}{name}"

    def _get_content_type(self, filename):
        """Get content type based on file extension"""
        ext = os.path.splitext(filename)[1].lower()
        content_types = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".gif": "image/gif",
            ".webp": "image/webp",
        }
        return content_types.get(ext, "application/octet-stream")
