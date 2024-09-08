
resource "google_compute_instance" "pruebavm" {
  count         = var.instancias
  name          = "worker-cpu-${count.index}"
  machine_type  = var.tipo_vm
  zone          = var.zone

  boot_disk {
    initialize_params {
      image = var.imagen
    }
  }

  network_interface {
    network = "default"
    access_config {}
  }

  metadata_startup_script =file(var.startup_worker_cpu)

#   metadata = {
#     ssh-keys = "${split("@", data.google_client_openid_userinfo.me.email)[0]}:${tls_private_key.ssh_key.public_key_openssh}"
#   } 
# }

# resource "google_compute_firewall" "allow-ssh" {
#   name    = "allow-ssh"
#   network = "default"

#   allow {
#     protocol = "tcp"
#     ports    = ["22"]
#   }

#   source_ranges = ["0.0.0.0/0"]
# }

# resource "google_compute_firewall" "allow-http" {
#   name    = "allow-http"
#   network = "default"

#   allow {
#     protocol = "tcp"
#     ports    = ["80"]
#   }

#   source_ranges = ["0.0.0.0/0"]
# }

# resource "google_compute_firewall" "allow-https" {
#   name    = "allow-https"
#   network = "default"

#   allow {
#     protocol = "tcp"
#     ports    = ["443"]
#   }

#   source_ranges = ["0.0.0.0/0"]
# }

# resource "tls_private_key" "ssh_key" {
#   algorithm   = "RSA"
#   rsa_bits    = 4096
# }
# resource "local_file" "ssh_private_key_pem" {
#   content         = tls_private_key.ssh_key.private_key_pem
#   filename        = ".ssh/google_compute_engine"
#   file_permission = "0600"
# }

}