const reverse = whatever =>{
    let reversed = ""
    for (i = whatever.length - 1;i >= 0 ; i--){
        reversed+=whatever[i]
    }
    return reversed
}
const count_char = (whatever,char) => {
    let count = 0;
    for (i = 0;i<whatever.length ; i++){
        if (whatever[i].toLowerCase() ==char.toLowerCase()){
            count++
        }
    }
    return count
}
const title = whatever => {
    let list = whatever.split(" ").map(el=> el[0].toUpperCase()+el.slice(1,el.length))
    return list.join(" ")
}
const maxMin = whatever => {
    max = whatever[0]
    min = whatever[0]
    for (el of whatever){
        if (max<el) {
            max = el
        }
        if (min > el) {
            min = el
        }
    }
    return [max,min]
}
const sum = whatever => whatever.reduce((el,acc) => acc + el,0)
const filter = (whatever,cond) => {
    let res = []
    for (el of whatever) {
        if (cond(el)){
            res.push(el)
        }
    }
    return res
}
const fact = num =>{
    let prod = 1
    for (let i = 1;i<=num;i++){
        prod*=i
    }
    return prod
}
const prime = num => {
    for (let i =2;i<=num/2;i++){
        if (num%i==0){
            return false
        }
    }
    return true
}
const fib = num => {
    if (num ===0 ){
        return 0
    }
    
    if (num ===1 ){
        return 1
    }
    
    return fib(num-1) + fib(num-2)
}
console.log(reverse("AYOUB"))
console.log(count_char("BARAA","A"))
console.log(title("ahla lila ahla nes"))
console.log(maxMin([1,2,3,4,5]))
console.log(sum([1,2,3,4,5]))
console.log(filter([1,2,3,4,5],x=>x>=3))
console.log(fact(4))
console.log(prime(2))
console.log(prime(16))
console.log(fib(8))
