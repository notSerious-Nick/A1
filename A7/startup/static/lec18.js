function doAsyncWork(resolve) {
    setTimeout(() => {
        resolve("done");
    }, 100);
}

function handleResult(result) {
    console.log(result);
}

const myPromise = new Promise(doAsyncWork);

myPromise.then(handleResult);
