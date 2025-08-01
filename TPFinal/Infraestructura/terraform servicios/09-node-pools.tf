
# resource "google_service_account" "kubernetes" {
#   account_id = "kubernetes"
# }

# resource "google_container_node_pool" "general" {
#   name       = "general"
#   cluster    = google_container_cluster.cluster-integrador.id
#   node_count = 0

#   management {
#     auto_repair  = true
#     auto_upgrade = true
#   }

#   autoscaling {
#     min_node_count = 1
#     max_node_count = 10
#   }

#   node_config {
#     preemptible  = false
#     machine_type = "e2-standard-4"

#     labels = {
#       role = "general"
#     }

#     service_account = google_service_account.kubernetes.email
#     oauth_scopes = [
#       "https://www.googleapis.com/auth/cloud-platform"
#     ]
#   }
# }

# resource "google_container_node_pool" "spot" {
#   name       = "spot"
#   cluster    = google_container_cluster.cluster-integrador.id
#   node_count = 2

#   management {
#     auto_repair  = true
#     auto_upgrade = true
#   }

#   autoscaling {
#     min_node_count = 2
#     max_node_count = 10
#   }

#   node_config {
#     preemptible  = true
#     machine_type = "e2-standard-4"

#     labels = {
#       team = "devops"
#     }

#     taint {
#       key    = "instance_type"
#       value  = "spot"
#       effect = "NO_SCHEDULE"
#     }

#     service_account = google_service_account.kubernetes.email
#     oauth_scopes = [
#       "https://www.googleapis.com/auth/cloud-platform"
#     ]
#   }
# }
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
