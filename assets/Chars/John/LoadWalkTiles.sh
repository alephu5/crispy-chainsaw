#! /usr/bin/bash
convert $1 -crop 64x64 +repage +adjoin tile_%02d.png 

mkdir -p Hurt/Down
mkdir -p Hurt/Left
mkdir -p Hurt/Right
mkdir -p Hurt/Up

mkdir -p Shoot/Down
mkdir -p Shoot/Left
mkdir -p Shoot/Right
mkdir -p Shoot/Up

mkdir -p Slash/Down
mkdir -p Slash/Left
mkdir -p Slash/Right
mkdir -p Slash/Up

mkdir -p Spellcast/Down
mkdir -p Spellcast/Left
mkdir -p Spellcast/Right
mkdir -p Spellcast/Up

mkdir -p Thrust/Down
mkdir -p Thrust/Left
mkdir -p Thrust/Right
mkdir -p Thrust/Up

mkdir -p Walk/Down
mkdir -p Walk/Left
mkdir -p Walk/Right
mkdir -p Walk/Up

# Walk
mv tile_130.png Walk/Down/tile_130.png
mv tile_131.png Walk/Down/tile_131.png
mv tile_132.png Walk/Down/tile_132.png
mv tile_133.png Walk/Down/tile_133.png
mv tile_134.png Walk/Down/tile_134.png
mv tile_135.png Walk/Down/tile_135.png
mv tile_136.png Walk/Down/tile_136.png
mv tile_137.png Walk/Down/tile_137.png
mv tile_138.png Walk/Down/tile_138.png

mv tile_117.png Walk/Left/tile_117.png
mv tile_118.png Walk/Left/tile_118.png
mv tile_119.png Walk/Left/tile_119.png
mv tile_120.png Walk/Left/tile_120.png
mv tile_121.png Walk/Left/tile_121.png
mv tile_122.png Walk/Left/tile_122.png
mv tile_123.png Walk/Left/tile_123.png
mv tile_124.png Walk/Left/tile_124.png
mv tile_125.png Walk/Left/tile_125.png

mv tile_143.png Walk/Right/tile_143.png
mv tile_144.png Walk/Right/tile_144.png
mv tile_145.png Walk/Right/tile_145.png
mv tile_146.png Walk/Right/tile_146.png
mv tile_147.png Walk/Right/tile_147.png
mv tile_148.png Walk/Right/tile_148.png
mv tile_149.png Walk/Right/tile_149.png
mv tile_150.png Walk/Right/tile_150.png
mv tile_151.png Walk/Right/tile_151.png

mv tile_104.png Walk/Up/tile_104.png
mv tile_105.png Walk/Up/tile_105.png
mv tile_106.png Walk/Up/tile_106.png
mv tile_107.png Walk/Up/tile_107.png
mv tile_108.png Walk/Up/tile_108.png
mv tile_109.png Walk/Up/tile_109.png
mv tile_110.png Walk/Up/tile_110.png
mv tile_111.png Walk/Up/tile_111.png
mv tile_112.png Walk/Up/tile_112.png
