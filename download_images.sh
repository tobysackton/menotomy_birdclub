#!/bin/bash
# Download images from the WordPress site into the images/ folder
# Run from the project root: bash download_images.sh

cd "$(dirname "$0")"
mkdir -p images

echo "Downloading homepage images..."

# Header logo (small)
curl -L -o images/logo.png \
  "https://bpx.ela.mybluehost.me/website_c5b9cabf/wp-content/uploads/2024/08/cropped-menotomy-bird-club-1.jpg"

# Large logo (homepage sidebar)
curl -L -o images/logo-large.png \
  "https://bpx.ela.mybluehost.me/website_c5b9cabf/wp-content/uploads/2024/08/menotomy-bird-club_sm.jpg"

# Group photo (20th anniversary)
curl -L -o images/group-photo.jpg \
  "https://bpx.ela.mybluehost.me/website_c5b9cabf/wp-content/uploads/2024/08/menotomy-bird-club-20th-391557594_697246699120351_6962077995899214006_n.jpg"

echo ""
echo "Done! Downloaded files:"
ls -lh images/
echo ""
echo "If any files are 0 bytes or very small, the URL may have changed."
echo "You can also right-click images on menotomybirdclub.com and 'Save Image As' directly."
