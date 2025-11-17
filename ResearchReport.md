# Object Storage Overview

## 1. Object Storage
Object Storage stores data in the form of **objects**, each containing:
- The **data** itself
- A **unique identifier**
- **Metadata**

Objects are stored in **buckets** instead of folders and are accessed via **APIs**.

**Advantages:**
- Highly scalable
- Fault-tolerant
- Cloud-friendly
- Easy to manage
- Ideal for backups and large datasets

**Disadvantages:**
- Higher latency at times
- Less convenient for frequent real-time edits compared to traditional file systems

**Other distributed storage systems:**
- **NAS:** Centralized file server accessible over the network. Simple to use, allows shared access, but has a single point of failure, limited scalability, and is not cloud-native.
- **HDFS:** Splits files into blocks and stores them across multiple servers with replication. Provides fault tolerance and supports parallel processing of large datasets, but is complex to manage, less flexible in cloud environments, and not suitable for small files.

**Summary:** NAS and HDFS were useful in the past, but today **object storage** is the most flexible and scalable solution for modern distributed, cloud-based systems.

---

## 2. S3 Storage Service
**S3** is a managed storage service by **Amazon Web Services (AWS)**, designed for storing files in an **Object Storage format**, accessible through a convenient and advanced **API**.

---

## 3. Buckets
**Buckets** are the basic containers that hold your data as objects.

---

## 4. Folder Structure
**No.** S3 does not use a real folder structure.  
Folders can be **simulated** using object names with certain patterns (prefix), but this is only a **UI or conceptual simulation**, not a true file system structure.

---

## 5. Data Limits
Traditional file systems have limitations such as disk size or file system limits.  
In S3, data is stored across multiple distributed servers, so there is **no overall size limit**, and each bucket can contain extremely large objects (up to **5TB per object** in S3).

---

## 6. S3-Compatible Services
- **Amazon S3 (AWS)** – the original service
- **MinIO** – open-source, standalone implementation compatible with S3
- **Ceph (RADOS Gateway)** – distributed storage system with S3 API support
- **Google Cloud Storage** – offers an S3-compatible interface in addition to its own API
- **Wasabi, Backblaze B2** – cloud storage providers with S3 interfaces

---

## 7. MinIO Docker Command
Run MinIO with Docker:

```bash
docker run \
  -p 9000:9000 \
  -p 9001:9001 \
  --name minio \
  -v ./data:/data \
  -e MINIO_ROOT_USER=admin \
  -e MINIO_ROOT_PASSWORD=password123 \
  minio/minio server /data --console-address ":9001"
