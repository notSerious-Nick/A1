let d1;
let d2;
let d3;

function data1() {
  setTimeout(() => {
    d1 = 1;
  }, 100);
}

function data2(result1) {
  setTimeout(() => {
    d2 = result1 + 2;
  }, 200);
}

function data3(result2) {
  setTimeout(() => {
    d3 = result2 + 3;
  }, 300);
}

d1 = data1();
d2 = data2(d1);
d3 = data3(d2);
console.log(d3);
