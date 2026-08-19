function redundant(str) {
    return function() {
        return str;
    };
}

const f = redundant("apple");
console.log(f());
