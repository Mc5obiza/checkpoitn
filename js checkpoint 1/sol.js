const bitwiseAND = (a,b) => {
    let a_bit = a.toString(2)
    console.log(a_bit)
    let b_bit = b.toString(2)
    console.log(b_bit)
    let maxLength = Math.max(a_bit.length, b_bit.length);
    a_bit = a_bit.padStart(maxLength, '0');
    b_bit = b_bit.padStart(maxLength, '0');
    let result = '';
    for (let i = 0; i < a_bit.length; i++) {
        if (a_bit[i] === '1' && b_bit[i] === '1') {
            result += '1';
        } else {
            result += '0';
        }
    }
    console.log(result)
    return parseInt(result, 2);
}
const bitwiseOR = (a,b) => {
    let a_bit = a.toString(2)
    console.log(a_bit)
    let b_bit = b.toString(2)
    console.log(b_bit)
    let maxLength = Math.max(a_bit.length, b_bit.length);
    a_bit = a_bit.padStart(maxLength, '0');
    b_bit = b_bit.padStart(maxLength, '0');
    let result = '';
    for (let i = 0; i < a_bit.length; i++) {
        if (a_bit[i] === '1' || b_bit[i] === '1') {
            result += '1';
        } else {
            result += '0';
        }
    }
    console.log(result)
    return parseInt(result, 2);
}
const bitwiseXOR = (a,b) => {
    let a_bit = a.toString(2)
    console.log(a_bit)
    let b_bit = b.toString(2)
    console.log(b_bit)
    let maxLength = Math.max(a_bit.length, b_bit.length);
    a_bit = a_bit.padStart(maxLength, '0');
    b_bit = b_bit.padStart(maxLength, '0');
    let result = '';
    for (let i = 0; i < a_bit.length; i++) {
        if (a_bit[i] === '1' && b_bit[i] === '0') {
            result += '1';
        } else if (a_bit[i] === '0' && b_bit[i] === '1') {
            result += '1';
        } else {
            result += '0';
        }
    }
    console.log(result)
    return parseInt(result, 2);
}
console.log(bitwiseAND(7, 12))
console.log(bitwiseOR(7, 12))
console.log(bitwiseXOR(7, 12))