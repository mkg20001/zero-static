#!/bin/sh

disable="Sidebar Trayicon CryptMessage Newsfeed Stats" #plugins that are disabled
language="en" #the language of the proxy
uiport="8899" #proxy port

##CODE##

usage() {
  echo
  echo "Usage: $0 <zite> [debug] [pack] [cleanbuild]"
  echo
  echo " debug           - Enable Debugging"
  echo " pack            - Create a ZeroStatic.tar.gz"
  echo " cleanbuild      - Remove everything except required files"
  echo " -h              - This help text."
  echo
}

parse_options() {
  set -- "$@"
  local ARGN=$#
  while [ "$ARGN" -ne 0 ]
  do
    if [ -z "$zite" ]; then
      zite="$1"
    else
      case $1 in
        -h) usage
            exit 0
        ;;
        debug) debug=true
        ;;
        pack) pack=true
        ;;
        cleanbuild) cleanbuild=true
        ;;
        ?*) echo "ERROR: Unknown option."
            usage
            exit 1
        ;;
      esac
    fi
    shift 1
    ARGN=$((ARGN-1))
  done
  if [ -z "$zite" ]; then
    usage
    exit 1
  fi
}

cleanbuild=false
pack=false
debug=false

parse_options "$@"


main=$(dirname $(readlink -f $0))
inject=$(dir -w 1 $main/plugins)
patches=$(dir -w 1 $main/patches)

if ! [ -e $main/ZeroNet ]; then
  echo "Please clone ZeroNet first into '$main/ZeroNet'"
  exit 2
fi

zerodir="$PWD/ZeroStatic"
zerosrc="$main/ZeroNet"

log() {
  echo "[$1] $2"
}

if [ -e $zerodir/data ] && ! $cleanbuild; then
  log "backup" "data directory"
  mv $zerodir/data $main/data
fi

if $debug; then
  disable=${disable//"Stats"/""}
fi

rm -rf $zerodir
cp -rp $zerosrc $zerodir

for d in $disable; do
  log "disable" "Plugin: $d"
  mv $zerodir/plugins/$d $zerodir/plugins/disabled-$d
done
for i in $inject; do
  log "inject" "Plugin: $i"
  cp -rp $main/plugins/$i $zerodir/plugins/$i
done

if [ -e $main/data ] && ! $cleanbuild; then
  log "restore" "data directory"
  mv $main/data $zerodir/data
fi

if $debug; then
  fport=15543
else
  fport=15541
fi

zeroargs="--fileserver_port $fport --batch --language $language --ui_port $uiport --homepage $zite"
if $debug; then
  zeroargs="$zeroargs --debug"
fi

zerocmd="python2 zeronet.py"

cd $zerodir

for p in $patches; do
  log "patch" "File: $p"
  git apply $main/patches/$p
done


if $cleanbuild; then
  keep="plugins src tools zeronet.py LICENSE requirements.txt"
  for f in * .[a-z][a-z]*; do
    del=true
    for k in $keep; do
      [ "$f" == "$k" ] && del=false
    done
    if $del; then
      log "cleanup" "File: $f"
      rm -rf $zerodir/$f
    fi
  done
fi

echo "$zerocmd $zeroargs" > $zerodir/start.sh

if $pack; then
  log "pack" "ZeroStatic.tar.gz"
  rm -f $zerodir.tar.gz
  tar cfz $zerodir.tar.gz .
fi

if $debug; then
  bash $zerodir/start.sh
fi
