function showTemporaryNotification() {
  let notification = document.querySelector("#notification");
  notification.textContent = "New order received!";
  setTimeout(() => {
    notification.textContent = "";
  }, 2000);
}

function moveToMyOrders(event) {
  let my_order = document.querySelector("#my-orders");
  if (event.target.tagName === "LI") {
    my_order.append(event.target);
  }
}

function moveToUnassignedOrders(event) {
  let unassigned_order = document.querySelector("#unassigned-orders");
  if (event.target.tagName === "LI") {
    unassigned_order.append(event.target);
  }
}

function filterCards() {
  let input = document.querySelector("#filter-text").value.toLowerCase();
  let cards = document.querySelectorAll(".order-card");

  cards.forEach((card) => {
    let cardName = card.querySelector(".item-name").textContent.toLowerCase();
    let shouldShow = cardName.includes(input);

    if (shouldShow) {
      card.classList.remove("hidden");
    } else {
      card.classList.add("hidden");
    }
  });
}

async function loadOrders() {
  let fetchError = document.querySelector("#fetch-error");
  let fetchedOrders = document.querySelector("#fetched-orders");
  try {
    fetchError.textContent = "";
    fetchedOrders.textContent = "Loading order...";
    let response = await fetch("/restaurant/orders-json/");
    if (!response.ok) {
      throw new Error("Request Failed");
    }
    let data = await response.json();
    fetchedOrders.textContent = "";

    data.orders.forEach((order) => {
      let card = document.createElement("div");
      card.classList.add("order-card");

      let itemName = document.createElement("h3");
      itemName.classList.add("item-name");
      itemName.textContent = order.item;

      let customer = document.createElement("p");
      customer.textContent = `Customer: ${order.customer_name}`;

      let table = document.createElement("p");
      table.textContent = `Table: ${order.table_number}`;

      let status = document.createElement("p");
      status.textContent = `Status: ${order.status}`;

      card.append(itemName);
      card.append(customer);
      card.append(table);
      card.append(status);

      fetchedOrders.append(card);
    });
    filterCards();
  } catch (error) {
    fetchedOrders.textContent = "";
    fetchError.textContent = "Could not load orders.";
  }
}

function setupPage() {
  let simulateButton = document.querySelector("#simulate-order-btn");
  let unassignedOrders = document.querySelector("#unassigned-orders");
  let myOrders = document.querySelector("#my-orders");
  let filterInput = document.querySelector("#filter-text");
  let loadOrdersButton = document.querySelector("#load-orders-btn");

  if (simulateButton) {
    simulateButton.addEventListener("click", showTemporaryNotification);
  }

  if (unassignedOrders) {
    unassignedOrders.addEventListener("click", moveToMyOrders);
  }

  if (myOrders) {
    myOrders.addEventListener("click", moveToUnassignedOrders);
  }

  if (filterInput) {
    filterInput.addEventListener("input", filterCards);
  }

  if (loadOrdersButton) {
    loadOrdersButton.addEventListener("click", loadOrders);
  }
}

setupPage();
