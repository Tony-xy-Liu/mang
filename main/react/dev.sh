HERE=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# npx create-react-app hello-world --template typescript
case $1 in
    -r )
    cd hello-world
    npm start
    ;;
esac
