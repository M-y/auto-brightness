#!/bin/bash
mkdir --parents autobrightness-0.1.0/tmp/autobrightness-0.1.0
find . -mindepth 1 -maxdepth 1 ! -regex '\(./.git\|./.gitignore\|./.vscode\|./.github\|./createdeb.sh\|./autobrightness-0.1.0\)' -exec cp -r {} autobrightness-0.1.0/tmp/autobrightness-0.1.0 \;
mkdir autobrightness-0.1.0/DEBIAN
echo "Package: autobrightness
Version: 0.1.0
Architecture: amd64
Depends: python3-pip
Maintainer: Muhammed YILDIRIM <ben@muhammed.im>
Description: Auto change screen brightness using webcam" > autobrightness-0.1.0/DEBIAN/control
echo "#!/bin/bash
pip install /tmp/autobrightness-0.1.0
rm -rf /tmp/autobrightness-0.1.0" > autobrightness-0.1.0/DEBIAN/postinst
chmod +x autobrightness-0.1.0/DEBIAN/postinst
dpkg-deb --build autobrightness-0.1.0
rm -rf autobrightness-0.1.0