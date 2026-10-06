output "bucket_name" {
  value = google_storage_bucket.siem_bucket.name
}

output "bigquery_analytics_dataset" {
  value = google_bigquery_dataset.analytics_dataset.dataset_id
}
