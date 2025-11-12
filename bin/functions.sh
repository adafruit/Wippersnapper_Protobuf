# functions to reuse in the build scripts

# delete and recreate the out directory
clean() {
  rm -rf $OUT_PATH
  mkdir $OUT_PATH
}

# activate mise for managing tool and library versions
activate_mise() {
  eval "$(mise activate bash)"
}

# checks to make sure a tool is on the path
# hints about mise install
ensure() {
  if ! which $1 &> /dev/null; then
    echo "Could not find $1 on the path! Did you run 'mise install'?"
    exit 1
  fi
}

# checks to ensure the nanopb submodule is populate
# hints how to git submodule
ensure_nanopb_submodule() {
  if ! ls nanopb/generator &> /dev/null; then
    printf "Did not find nanopb files in the repo! Did you init submodules?\ngit submodule init\ngit submodule update\n"
    exit 1
  fi
}

# message to signify completion
completed_message() {
  echo "Built $1 wrappers to $OUT_PATH/"
}
