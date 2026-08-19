const getNotesDistribution = (notes) => {
    let count = {}
    for (let el of notes){
        count = el.notes.filter(x => x >=1 && x<=5).reduce((counts,note) => {
            counts[note] = (counts[note] || 0) + 1
            return counts
        },count)
    }
    return count
}
console.log(getNotesDistribution([
  {
    "name": "Steve",
    "notes": [5, 5, 3, -1, 6]
  },
  {
    "name": "John",
    "notes": [3, 2, 5, 0, -3]
  }
]
))