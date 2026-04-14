#!/bin/bash
# Bulk download all WordPress media library images
# Run from project root: bash download_all_images.sh

cd "$(dirname "$0")"
mkdir -p images

echo "Downloading all 50 WordPress media files..."
echo "============================================"

# -- LOGOS & GROUP PHOTO (essential) --
curl -L -s -o "images/cropped-menotomy-bird-club-1.jpg" "https://menotomybirdclub.com/wp-content/uploads/2024/08/cropped-menotomy-bird-club-1.jpg" && echo "OK: cropped-menotomy-bird-club-1.jpg"

# -- SCREENSHOTS (maps, locations, etc.) --
curl -L -s -o "images/Screenshot-2025-06-12-at-2.05.19-PM.png" "https://menotomybirdclub.com/wp-content/uploads/2024/10/Screenshot-2025-06-12-at-2.05.19%20PM.png" && echo "OK: Screenshot-2025-06-12-at-2.05.19-PM.png"
curl -L -s -o "images/Screenshot-2025-04-27-at-12.42.31-PM.png" "https://menotomybirdclub.com/wp-content/uploads/2025/03/Screenshot-2025-04-27-at-12.42.31%20PM.png" && echo "OK: Screenshot-2025-04-27-at-12.42.31-PM.png"
curl -L -s -o "images/Screenshot-2024-09-24-at-3.42.46-PM.png" "https://menotomybirdclub.com/wp-content/uploads/2024/09/Screenshot-2024-09-24-at-3.42.46%20PM.png" && echo "OK: Screenshot-2024-09-24-at-3.42.46-PM.png"
curl -L -s -o "images/Screenshot-2024-09-24-at-3.39.01-PM.jpg" "https://menotomybirdclub.com/wp-content/uploads/2024/09/Screenshot-2024-09-24-at-3.39.01%20PM.jpg" && echo "OK: Screenshot-2024-09-24-at-3.39.01-PM.jpg"
curl -L -s -o "images/Screenshot-2024-09-24-at-3.26.14-PM.png" "https://menotomybirdclub.com/wp-content/uploads/2024/09/Screenshot-2024-09-24-at-3.26.14%20PM.png" && echo "OK: Screenshot-2024-09-24-at-3.26.14-PM.png"
curl -L -s -o "images/Screenshot-2024-09-11-at-12.42.38-PM.png" "https://menotomybirdclub.com/wp-content/uploads/2024/09/Screenshot-2024-09-11-at-12.42.38%20PM.png" && echo "OK: Screenshot-2024-09-11-at-12.42.38-PM.png"
curl -L -s -o "images/Screenshot-2024-09-10-at-3.53.24-PM.png" "https://menotomybirdclub.com/wp-content/uploads/2024/09/Screenshot-2024-09-10-at-3.53.24%20PM.png" && echo "OK: Screenshot-2024-09-10-at-3.53.24-PM.png"
curl -L -s -o "images/Screenshot-2024-09-10-at-3.48.50-PM.png" "https://menotomybirdclub.com/wp-content/uploads/2024/09/Screenshot-2024-09-10-at-3.48.50%20PM.png" && echo "OK: Screenshot-2024-09-10-at-3.48.50-PM.png"
curl -L -s -o "images/Screenshot-2024-09-10-at-3.38.15-PM.png" "https://menotomybirdclub.com/wp-content/uploads/2024/09/Screenshot-2024-09-10-at-3.38.15%20PM.png" && echo "OK: Screenshot-2024-09-10-at-3.38.15-PM.png"
curl -L -s -o "images/Screenshot-2024-09-07-at-9.59.20-PM.png" "https://menotomybirdclub.com/wp-content/uploads/2024/09/Screenshot-2024-09-07-at-9.59.20%20PM.png" && echo "OK: Screenshot-2024-09-07-at-9.59.20-PM.png"
curl -L -s -o "images/Screenshot-2024-08-12-at-11.02.45-AM.png" "https://menotomybirdclub.com/wp-content/uploads/2024/08/Screenshot-2024-08-12-at-11.02.45%20AM.png" && echo "OK: Screenshot-2024-08-12-at-11.02.45-AM.png"
curl -L -s -o "images/Screenshot-2024-04-17-at-12.17.40-PM.png" "https://menotomybirdclub.com/wp-content/uploads/2024/08/Screenshot-2024-04-17-at-12.17.40%20PM.png" && echo "OK: Screenshot-2024-04-17-at-12.17.40-PM.png"
curl -L -s -o "images/Screenshot-2024-04-17-at-9.57.08-AM.png" "https://menotomybirdclub.com/wp-content/uploads/2024/08/Screenshot-2024-04-17-at-9.57.08%20AM.png" && echo "OK: Screenshot-2024-04-17-at-9.57.08-AM.png"
curl -L -s -o "images/Screenshot-2024-04-17-at-9.48.36-AM.png" "https://menotomybirdclub.com/wp-content/uploads/2024/08/Screenshot-2024-04-17-at-9.48.36%20AM.png" && echo "OK: Screenshot-2024-04-17-at-9.48.36-AM.png"

# -- BIRD & TRIP PHOTOS --
curl -L -s -o "images/075405b0cc31c7a-greenwood-park.jpg" "https://menotomybirdclub.com/wp-content/uploads/2024/09/075405b0cc31c7a08e1850530642882b89a36e29e84a537482e5b4290674d7ed-rimg-w1200-h900-dc332b13-gmir.jpg" && echo "OK: greenwood-park.jpg"
curl -L -s -o "images/Bombus_vagans_800.jpg" "https://menotomybirdclub.com/wp-content/uploads/2024/10/Bombus_vagans_800.jpg" && echo "OK: Bombus_vagans_800.jpg"
curl -L -s -o "images/4-9-25-Brooks-Estate-Medford.jpg" "https://menotomybirdclub.com/wp-content/uploads/2025/04/4-9-25-Menotomy-BBC-Brooks-Estate-Medford-241.jpg" && echo "OK: Brooks-Estate-Medford.jpg"
curl -L -s -o "images/greenough_land_carlisle.jpg" "https://menotomybirdclub.com/wp-content/uploads/2024/09/greenough_land_carlisle-scaled.jpg" && echo "OK: greenough_land_carlisle.jpg"
curl -L -s -o "images/IMG_7958_sm.jpg" "https://menotomybirdclub.com/wp-content/uploads/2024/10/IMG_7958_sm.jpg" && echo "OK: IMG_7958_sm.jpg"
curl -L -s -o "images/sm-20111104-IMG_2124.jpg" "https://menotomybirdclub.com/wp-content/uploads/2025/01/sm-20111104-20111104-IMG_2124.jpg" && echo "OK: sm-20111104-IMG_2124.jpg"
curl -L -s -o "images/20111104-IMG_2124.jpg" "https://menotomybirdclub.com/wp-content/uploads/2025/01/20111104-20111104-IMG_2124.jpg" && echo "OK: 20111104-IMG_2124.jpg"
curl -L -s -o "images/EC5_3121-Enhanced-NR-X5.jpg" "https://menotomybirdclub.com/wp-content/uploads/2024/11/EC5_3121-Enhanced-NR-X5.jpg" && echo "OK: EC5_3121-Enhanced-NR-X5.jpg"
curl -L -s -o "images/BlacksNook-1.jpg" "https://menotomybirdclub.com/wp-content/uploads/2024/10/BlacksNook-1.jpg" && echo "OK: BlacksNook-1.jpg"
curl -L -s -o "images/BlacksNook-scaled.jpg" "https://menotomybirdclub.com/wp-content/uploads/2024/10/BlacksNook-scaled.jpg" && echo "OK: BlacksNook-scaled.jpg"
curl -L -s -o "images/464419054-horn-pond.jpg" "https://menotomybirdclub.com/wp-content/uploads/2024/10/464419054_926059589572393_7859313205872424834_n.jpg" && echo "OK: horn-pond.jpg"
curl -L -s -o "images/20220502-354A8545-spotted-sandpiper.jpg" "https://menotomybirdclub.com/wp-content/uploads/2024/10/20220502-354A8545-Edit.jpg" && echo "OK: spotted-sandpiper.jpg"
curl -L -s -o "images/Wright-Locke-Farm-Winchester.jpg" "https://menotomybirdclub.com/wp-content/uploads/2024/09/9-24-24-Wright-Locke-Farm-Winchester-Lisa-leading-Menotomy-Bird-Club-58.jpg" && echo "OK: Wright-Locke-Farm-Winchester.jpg"
curl -L -s -o "images/squantum-point-park.jpg" "https://menotomybirdclub.com/wp-content/uploads/2024/09/squantum-point-park.jpg" && echo "OK: squantum-point-park.jpg"
curl -L -s -o "images/carlisle-cranberry-bog.jpg" "https://menotomybirdclub.com/wp-content/uploads/2024/09/carlisle-cranberry-bog.jpg" && echo "OK: carlisle-cranberry-bog.jpg"
curl -L -s -o "images/horn-pond-community-garden.jpg" "https://menotomybirdclub.com/wp-content/uploads/2024/09/horn-pond-community-garden-e1727269334788.jpg" && echo "OK: horn-pond-community-garden.jpg"
curl -L -s -o "images/20210611-354A0946.jpg" "https://menotomybirdclub.com/wp-content/uploads/2024/09/20210611-354A0946.jpg" && echo "OK: 20210611-354A0946.jpg"
curl -L -s -o "images/Arlington-Reservoir-David-White.jpg" "https://menotomybirdclub.com/wp-content/uploads/2024/09/Arlington-Reservoir-David-White-2048x982-1.jpg" && echo "OK: Arlington-Reservoir-David-White.jpg"
curl -L -s -o "images/Foss_Farm_Carlisle_MA.jpg" "https://menotomybirdclub.com/wp-content/uploads/2024/09/Foss_Farm_Carlisle_MA.jpg" && echo "OK: Foss_Farm_Carlisle_MA.jpg"
curl -L -s -o "images/20240904-_51A1613-rose-breasted-grosbeak.jpg" "https://menotomybirdclub.com/wp-content/uploads/2024/09/20240904-_51A1613-Edit.jpg" && echo "OK: rose-breasted-grosbeak.jpg"
curl -L -s -o "images/20240904-_51A1594-warbler.jpg" "https://menotomybirdclub.com/wp-content/uploads/2024/09/20240904-_51A1594.jpg" && echo "OK: warbler-1594.jpg"
curl -L -s -o "images/20240904-_51A1558-warbler.jpg" "https://menotomybirdclub.com/wp-content/uploads/2024/09/20240904-_51A1558.jpg" && echo "OK: warbler-1558.jpg"
curl -L -s -o "images/BNC_KForesto-red-bellied-woodpecker.jpg" "https://menotomybirdclub.com/wp-content/uploads/2024/09/0dabf6c79513-BNC_KForesto-0990-1920x1280-1.jpg" && echo "OK: red-bellied-woodpecker.jpg"
curl -L -s -o "images/BelleIsleMarsh1Alc.jpg" "https://menotomybirdclub.com/wp-content/uploads/2024/09/BelleIsleMarsh1Alc.jpg" && echo "OK: BelleIsleMarsh1Alc.jpg"
curl -L -s -o "images/20210919-354A2870-2.jpg" "https://menotomybirdclub.com/wp-content/uploads/2024/09/20210919-354A2870-2.jpg" && echo "OK: 20210919-354A2870-2.jpg"
curl -L -s -o "images/20210919-354A2870.jpg" "https://menotomybirdclub.com/wp-content/uploads/2024/09/20210919-354A2870.jpg" && echo "OK: 20210919-354A2870.jpg"
curl -L -s -o "images/IMG_3182-1.jpg" "https://menotomybirdclub.com/wp-content/uploads/2024/08/IMG_3182-1.jpg" && echo "OK: IMG_3182-1.jpg"
curl -L -s -o "images/IMG_3182-scaled.jpg" "https://menotomybirdclub.com/wp-content/uploads/2024/08/IMG_3182-scaled.jpg" && echo "OK: IMG_3182-scaled.jpg"
curl -L -s -o "images/20240410-_51A5698-Edit.jpg" "https://menotomybirdclub.com/wp-content/uploads/2024/08/20240410-_51A5698-Edit.jpg" && echo "OK: 20240410-_51A5698-Edit.jpg"
curl -L -s -o "images/20240402-_51A5384-scaled.jpg" "https://menotomybirdclub.com/wp-content/uploads/2024/08/20240402-_51A5384-scaled.jpg" && echo "OK: 20240402-_51A5384-scaled.jpg"
curl -L -s -o "images/20240410-_51A5678-Edit-scaled.jpg" "https://menotomybirdclub.com/wp-content/uploads/2024/08/20240410-_51A5678-Edit-scaled.jpg" && echo "OK: 20240410-_51A5678-Edit-scaled.jpg"

echo ""
echo "============================================"
echo "Download complete!"
echo ""
echo "Skipped (not real image URLs):"
echo "  - IMG_7958.heic (unsupported format)"
echo "  - http://Image%20of%20Rufous%20Motmot... (broken URL)"
echo "  - chatgeo.photos external links x2 (external site)"
echo ""
echo "Downloaded files:"
ls -1 images/ | wc -l
echo "files in images/"
echo ""
du -sh images/
