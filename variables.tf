variable "LOCATION" {
  description = "The Azure location where all resources in this deployment should be created"
  default = "uksouth"   
}
variable "CLIENT_ID" {
    description = "The GitHub Client ID"
    default = "$VARIABLE_CLIENT_ID"
}
variable "CLIENT_SECRET" {
    description = "The GitHub Client secret"
    default = "$VARIABLE_CLIENT_SECRET"
}
variable "SECRET_KEY" {
    description = "Top secret key"
    default = "$VARIABLE_SECRET_KEY"
}