from minio import Minio
from dotenv import load_dotenv
import os
import io
import random
import string
import logging
from minio.error import S3Error

logging.basicConfig(level=logging.INFO)

load_dotenv()


# -----------------------
# Setup MinIO client
# -----------------------
def setup_client():
    endpoint = os.getenv("MINIO_ENDPOINT", "localhost:9000")
    access_key = os.getenv("MINIO_ACCESS_KEY")
    secret_key = os.getenv("MINIO_SECRET_KEY")
    secure = os.getenv("MINIO_SECURE") == "True"

    if not access_key or not secret_key:
        raise ValueError("MINIO_ACCESS_KEY and MINIO_SECRET_KEY must be set")

    return Minio(
        endpoint=endpoint,
        access_key=access_key,
        secret_key=secret_key,
        secure=secure
    )


# -----------------------
# Utility functions
# -----------------------
def random_name(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


def random_data(size=100):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=size)).encode('utf-8')


def create_bucket_if_not_exists(client, bucket_name):
    try:
        if not client.bucket_exists(bucket_name):
            client.make_bucket(bucket_name)
            logging.info(f"📦 Bucket '{bucket_name}' created.")
    except S3Error as e:
        logging.error(f"❌ Failed to create/check bucket '{bucket_name}': {e}")
    except Exception as e:
        logging.error(f"❌ Unexpected error: {e}")


def upload_object(client, bucket_name, object_name, data):
    client.put_object(
        bucket_name,
        object_name,
        io.BytesIO(data),
        length=len(data),
        content_type="text/plain"
    )
    logging.info(f"✅ Uploaded object '{object_name}' with random data.")


def list_objects(client, bucket_name):
    objects = client.list_objects(bucket_name, recursive=True)
    logging.info("📦 Objects in bucket:")
    for obj in objects:
        logging.info(f"- {obj.object_name} ({obj.size} bytes)")


def read_object(client, bucket_name, object_name):
    with client.get_object(bucket_name, object_name) as response:
        data = response.read().decode("utf-8")
    logging.info(f"📄 Content of {object_name}:")
    logging.info(data)
    return data


def remove_object(client, bucket_name, object_name):
    client.remove_object(bucket_name, object_name)
    logging.info(f"🗑️ Object '{object_name}' removed successfully.")


def update_object(client, bucket_name, object_name, new_data_bytes):
    new_data = io.BytesIO(new_data_bytes)
    client.put_object(
        bucket_name,
        object_name,
        new_data,
        length=len(new_data.getvalue()),
        content_type="text/plain"
    )
    logging.info(f"📝 Object '{object_name}' updated.")


# -----------------------
# Run code only if executed directly
# -----------------------
if __name__ == "__main__":
    client = setup_client()
    bucket_name = "mybucket"
    object_name = f"{random_name()}.txt"
    data = random_data(50)

    create_bucket_if_not_exists(client, bucket_name)
    upload_object(client, bucket_name, object_name, data)
    list_objects(client, bucket_name)
    read_object(client, bucket_name, object_name)
    remove_object(client, bucket_name, object_name)
    update_object(client, bucket_name, object_name, b"This is the updated data.")
