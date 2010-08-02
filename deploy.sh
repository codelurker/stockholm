#!/bin/bash
echo 
echo "##############################"
echo "Deploying new version of branch" 
git branch | grep "*"
echo "##############################"
echo 


clean=$(git status | grep -c "working directory clean")
[ "$clean" == "1" ] || {
  echo "Commit your changes first"
  exit
}

git log -n 1 | head -1 >version.txt

echo last commit
cat version.txt
echo

appcfg.py update ../stockholm/ -e robcos@robcos.com
