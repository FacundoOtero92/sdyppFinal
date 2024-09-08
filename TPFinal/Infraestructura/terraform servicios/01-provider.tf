provider "google" {
  credentials = file("${path.module}/credentials.json")
  project     = var.project_id
  zone        = var.zone
  region      = var.region
}
