
 resource "google_service_account" "kubernetes" {
   account_id = "kubernetes"
 }


# Node Pool para aplicaciones (ej: coordinador, workers)
resource "google_container_node_pool" "apps_pool" {
  name       = "apps-pool"
  cluster    = google_container_cluster.cluster-integrador.id
  location   = var.region
  node_count = 1

  autoscaling {
    min_node_count = 1
    max_node_count = 4

  }

  management {
    auto_repair  = true
    auto_upgrade = true
  }

  node_config {
    machine_type = "e2-standard-4"
    labels = {
      type = "aplicacion"
    }
    service_account = google_service_account.kubernetes.email
    oauth_scopes = ["https://www.googleapis.com/auth/cloud-platform"]
  }
}

# Node Pool para servicios (ej: Redis, RabbitMQ)
resource "google_container_node_pool" "services_pool" {
  name       = "services-pool"
  cluster    = google_container_cluster.cluster-integrador.id
  location   = var.region
  node_count = 1

  autoscaling {
    min_node_count = 1
    max_node_count = 4
  }

  management {
    auto_repair  = true
    auto_upgrade = true
  }

  node_config {
    machine_type = "e2-medium"
    labels = {
       type = "servicio"
    }
    service_account = google_service_account.kubernetes.email
    oauth_scopes = ["https://www.googleapis.com/auth/cloud-platform"]
  }
}
