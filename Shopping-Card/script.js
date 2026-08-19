const products = document.querySelectorAll('.list-products > .card-body');
const totalDisplay = document.querySelector('.total-price .total');
function updateTotal() {
  let total = 0;
  products.forEach((product) => {
    if (product.dataset.deleted === 'true') return;
    const unitPrice = parseFloat(product.querySelector('.unit-price').textContent);
    const quantity = parseInt(product.querySelector('.quantity').textContent, 10);
    total += unitPrice * quantity;
  });
  totalDisplay.textContent = `${total} $`;
}
products.forEach((product) => {
  const plusBtn = product.querySelector('.fa-plus-circle');
  const minusBtn = product.querySelector('.fa-minus-circle');
  const quantitySpan = product.querySelector('.quantity');
  const trashBtn = product.querySelector('.fa-trash-alt');
  const heartBtn = product.querySelector('.fa-heart');
  plusBtn.addEventListener('click', () => {
    const quantity = parseInt(quantitySpan.textContent, 10) + 1;
    quantitySpan.textContent = quantity;
    updateTotal();
  });
  minusBtn.addEventListener('click', () => {
    const current = parseInt(quantitySpan.textContent, 10);
    const quantity = current > 0 ? current - 1 : 0;
    quantitySpan.textContent = quantity;
    updateTotal();
  });
  trashBtn.addEventListener('click', () => {
    product.dataset.deleted = 'true';
    product.style.display = 'none';
    updateTotal();
  });
  heartBtn.addEventListener('click', () => {
    heartBtn.classList.toggle('liked');
    heartBtn.style.color = heartBtn.classList.contains('liked') ? '#e63946' : '';
  });
});
updateTotal();