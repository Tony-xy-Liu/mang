HERE=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# npm install -g @vue/cli
# vue create hello-world
# npm install bootstrap
# npm install bootstrap-icons
case $1 in
    -r )
    cd hello-world
    npm run serve
    ;;
esac
