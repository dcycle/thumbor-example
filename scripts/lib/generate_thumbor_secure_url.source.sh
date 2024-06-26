# Generate secure Thumbor URL
#
# unsafe_url_part=500x/www.example.com/large-image.jpg
#
# usage:
#   source .env
#   unsafe_url_part=500x/www.example.com/large-image.jpg
#   key=$THUMBOR_SECURITY_KEY
#   secure_key = $(generate_thumbor_secure_url "$unsafe_url_part" "$key")
#
# full_path = http://images.example.com/$secure_key/$unsafe_url_part
#

generate_thumbor_secure_url() {
  local unsafe_part="$1"
  local security_key="$2"

  # Calculate HMAC-SHA1 signature with base 64 encoded
  local signature=$(echo -n "$unsafe_part" | openssl dgst -sha1 -hmac "$security_key" -binary | base64 | tr '+/' '-_' )
  echo "$signature"  # Return the value instead of echoing it
}
