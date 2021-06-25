variable "location" {
  description = "The Azure location where all resources in this deployment should be created"
  default = "uksouth"   
}
variable "client_id" {
  description = "The client ID"
  default = "$variables_client_id"
}
variable "client_secret"  {
  description = "The client secret"
  default = "$variables_client_secret"
}