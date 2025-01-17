APP_NAME=MediaInfo
APP_ICON=MediaInfo.icns

cd "$(dirname "$0")"

rm -R "dist/$APP_NAME" 2>/dev/null
rm -R "dist/$APP_NAME.app" 2>/dev/null
rm -R "dist/$APP_NAME.dmg" 2>/dev/null

echo
echo '****************************************'
echo 'Checking requirements...'
echo '****************************************'

pip install -r requirements_macos.txt
pip install -r requirements_dist.txt

echo
echo '****************************************'
echo 'Running pyinstaller...'
echo '****************************************'

#pyinstaller --noupx -w -i "$APP_ICON" -n "$APP_NAME" -D main.py --exclude-module _bootlocale
pyinstaller "${APP_NAME}_macos.spec"

echo
echo '****************************************'
echo 'Copying resources...'
echo '****************************************'

cp resources/mediainfo "dist/$APP_NAME.app/Contents/Resources/"

echo
echo '****************************************'
echo 'Optimizing application...'
echo '****************************************'

rm "dist/$APP_NAME.app/Contents/Frameworks/libcrypto.3.dylib"
rm "dist/$APP_NAME.app/Contents/Frameworks/libssl.3.dylib"
rm "dist/$APP_NAME.app/Contents/Resources/libcrypto.3.dylib"
rm "dist/$APP_NAME.app/Contents/Resources/libssl.3.dylib"

echo
echo '****************************************'
echo 'Creating DMG...'
echo '****************************************'
mkdir dist/dmg
mv "dist/$APP_NAME.app" dist/dmg/
ln -s /Applications "dist/dmg/Applications"
hdiutil create -fs HFSX -format UDZO "dist/$APP_NAME.dmg" -imagekey zlib-level=9 -srcfolder "dist/dmg" -volname "$APP_NAME"
mv "dist/dmg/$APP_NAME.app" dist/
rm -R dist/dmg

echo
echo '****************************************'
echo 'Done.'
echo '****************************************'
echo
