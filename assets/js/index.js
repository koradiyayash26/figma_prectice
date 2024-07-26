function demo(rows) {
    for (let i = 0; i < rows; i++) {
        let row = '';
        for (let j = 0; j <= i; j++) {
            if (j === 0 || j === i) {
                row += '1 ';
            } else {
                row += `${cal(i, j)} `;
            }
        }
        console.log(row);
    }
}
function cal(i, j) {
    return factorial(i) / (factorial(j) * factorial(i - j));
}
function factorial(n) {
    if (n === 0 || n === 1) {
        return 1;
    } else {
        return n * factorial(n - 1);
    }
}
demo(5);








