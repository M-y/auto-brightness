#!/bin/bash
VER=$1
mkdir --parents "deb/tmp/autobrightness-$VER"
find . -mindepth 1 -maxdepth 1 ! -regex '\(./.git\|./.gitignore\|./.vscode\|./.github\|./createdeb.sh\|./deb\)' -exec cp -r {} "deb/tmp/autobrightness-$VER" \;
mkdir deb/DEBIAN
echo "Package: autobrightness
Version: $VER
Architecture: amd64
Depends: python3-pip
Maintainer: Muhammed YILDIRIM <ben@muhammed.im>
Description: Auto change screen brightness using webcam" > deb/DEBIAN/control
echo "#!/bin/bash
pip install /tmp/autobrightness-$VER
rm -rf /tmp/autobrightness-$VER
echo \"[Desktop Entry]
Name=autobrightness
Type=Application
Exec=sudo autobrightness
Terminal=false\" > /etc/xdg/autostart/autobrightness.desktop
echo \"%sudo   ALL=(ALL:ALL) NOPASSWD: \$(which autobrightness)\" > /etc/sudoers.d/autobrightness" > deb/DEBIAN/postinst
chmod +x deb/DEBIAN/postinst
dpkg-deb --build deb "autobrightness-$VER.deb"
rm -rf deb