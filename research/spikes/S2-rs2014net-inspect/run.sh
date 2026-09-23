#!/usr/bin/env bash
# Spike S2: static inspection of Rocksmith2014.NET at a pinned commit.
# Verifies: license, target framework, PSARC/SNG cipher modes, supported Wwise versions,
# availability of package builder / DD generator / phrase generator / arrangement checker.
set -eu
PIN=b87c9a3afd31c40ade9685a9244e718e7581c0cb
D=$(mktemp -d); git clone -q https://github.com/iminashi/Rocksmith2014.NET "$D/rs"; cd "$D/rs"; git checkout -q "$PIN"
echo "commit: $(git rev-parse HEAD) ($(git log -1 --format=%cd))"
echo "license: $(head -1 LICENSE)"
echo "target frameworks:"; grep -h "<TargetFramework>" src/*/*.fsproj | sort | uniq -c
echo "PSARC cipher:"; grep -n "CipherMode" src/Rocksmith2014.PSARC/Cryptography.fs
echo "SNG cipher:";   grep -n "AES CTR" src/Rocksmith2014.SNG/Cryptography.fs
echo "Wwise versions accepted:"; grep -n 'Regex.IsMatch(fn' src/Rocksmith2014.Audio/Wwise/WwiseFinder.fs
echo "Wwise on Linux:"; grep -n "wine" src/Rocksmith2014.Audio/Wwise/WwiseFinder.fs
echo "APIs:"
grep -n "^let buildPackages" src/Rocksmith2014.DLCProject/PackageBuilder.fs
grep -n "^let generateForArrangement" src/Rocksmith2014.DD/Generator.fs
ls src/Rocksmith2014.XML.Processing/ | grep -E "PhraseGenerator|ArrangementChecker"
grep -n "let save\|let load" src/Rocksmith2014.DLCProject/DLCProject.fs
