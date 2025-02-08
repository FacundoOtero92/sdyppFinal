# # https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/google_project_service
resource "google_project_service" "compute" {
  service = "compute.googleapis.com"
  lifecycle {
    prevent_destroy = true
    ignore_changes = [
      name,
      auto_create_subnetworks
    ]
  }

}


resource "google_project_service" "container" {
  service = "container.googleapis.com"
  lifecycle {
    prevent_destroy = true
    ignore_changes = [
      name,
      auto_create_subnetworks
    ]
  }
}

resource "google_project_service" "cloud_resource_manager" {
  service            = "cloudresourcemanager.googleapis.com"
  disable_on_destroy = false
  lifecycle {
    prevent_destroy = true
    ignore_changes = [
      name,
      auto_create_subnetworks
    ]
  }
}
