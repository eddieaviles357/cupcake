const $ckList = $('#cupcakes-list')
const $getCupcakesBtn = $('#get-cupcakes')

$getCupcakesBtn.click(getCupcakes)

async function getCupcakes() {
    const {data} = await axios.get("/api/cupcakes")
    console.log(data.cupcakes)
    console.log($ckList)
    for (cupcake of data.cupcakes) {
        console.log(cupcake)
        $ckList.append(
            `<li>
                <div>Id: ${cupcake.id}</div>
                <div>Flavor: ${cupcake.flavor}</div>
                <div>Size: ${cupcake.size}</div>
                <div>Rating: ${cupcake.rating}</div>
                <div>Image: ${cupcake.image}</div>
            </li>`)
    }
}