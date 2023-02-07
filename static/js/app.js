const $ckList = $('#cupcakes-list')
const $getCupcakesBtn = $('#get-cupcakes')
const $formCupcake = $('#form-cupcake')
const $flavor = $('#flavor')
const $size = $('#size')
const $rating = $('#rating')
const $image = $('#image')

$getCupcakesBtn.click(getCupcakes)

async function getCupcakes() {
    const {data} = await axios.get("/api/cupcakes")
    // clear list of cupcakes
    $ckList.children().remove();
    // append list of cupcakes to list container
    for (ck of data.cupcakes) {
        $ckList.append(createCupcakeLI(ck.flavor, ck.size, ck.rating, ck.image));
    }
}

$formCupcake.submit(submitCK)
let form = null
async function submitCK(e) {
    e.preventDefault()
    
    ck = {
        "flavor": $flavor.val(),
        "size": $size.val(),
        "rating": Number($rating.val()),
        "image": $image.val()
    }
    resp = axios.post("/api/cupcakes", ck)
    console.log(resp)
    $ckList.append(createCupcakeLI(ck.flavor, ck.size, ck.rating, ck.image));
}

// create <li>with cupcake data</li>
function createCupcakeLI(flavor,size,rating,image) {
    return `<li class="mt-3 mb-3 p-3 list-group-item list-group-item-secondary w-25">
                <div class="d-inline">
                    <div>Flavor: ${flavor}</div>
                    <div>Size: ${size}</div>
                    <div>Rating: ${rating}</div>
                </div>
                <div class="">
                    <image src=${image} class="img-thumbnail" />
                </div>
            </li>`
}