const API_BASE_URL = "https://staff-directory.onrender.com";
const RANDOM_USER_URL = "https://randomuser.me/api/?results=10";

let allStaff = [];

const staffContainer = document.getElementById("staffContainer");
const statusMessage = document.getElementById("statusMessage");
const searchInput = document.getElementById("searchInput");
const areaFilter = document.getElementById("areaFilter");
const modalName = document.getElementById("modalName");
const modalBody = document.getElementById("modalBody");
const staffModal = new bootstrap.Modal(document.getElementById("staffModal"));

document.addEventListener("DOMContentLoaded", loadStaffDirectory);

async function loadStaffDirectory() {
  showStatus("Loading staff directory...", "info");

  try {
    const [randomUserResponse, ownApiResponse] = await Promise.all([
      fetch(RANDOM_USER_URL),
      fetch(`${API_BASE_URL}/staff`),
    ]);

    if (!randomUserResponse.ok) {
      throw new Error(
        `randomuser.me request failed (status ${randomUserResponse.status})`
      );
    }
    if (!ownApiResponse.ok) {
      throw new Error(
        `Own API request failed (status ${ownApiResponse.status})`
      );
    }

    const randomUserData = await randomUserResponse.json();
    const ownApiData = await ownApiResponse.json();

    const randomUsers = randomUserData.results;
    const staffExtras = ownApiData;

    allStaff = randomUsers.map((user, index) => {
      const extra = staffExtras[index] || {};
      return {
        id: extra.id ?? index,
        name: `${user.name.first} ${user.name.last}`,
        image: user.picture.large,
        email: extra.email || user.email,
        jobTitle: extra.job_title || "Unknown role",
        researchArea: extra.research_area || "Unspecified",
        phone: user.phone,
        location: `${user.location.city}, ${user.location.country}`,
      };
    });

    populateAreaFilter(allStaff);
    renderStaff(allStaff);
    clearStatus();
  } catch (error) {
    console.error("Failed to load staff directory:", error);
    showStatus(
      "Sorry, we couldn't load the staff directory right now. Please check your connection and that the backend server is running, then refresh the page.",
      "danger"
    );
  }
}

function createStaffCard(person) {
  const col = document.createElement("div");
  col.className = "col-sm-6 col-md-4 col-lg-3";

  col.innerHTML = `
    <div class="card staff-card" data-id="${person.id}">
      <img src="${person.image}" alt="Photo of ${person.name}" />
      <div class="card-body">
        <h5 class="card-title mb-1">${person.name}</h5>
        <p class="card-text text-muted mb-1">${person.jobTitle}</p>
        <p class="card-text small">${person.researchArea}</p>
      </div>
    </div>
  `;

  col
    .querySelector(".staff-card")
    .addEventListener("click", () => openStaffModal(person));

  return col;
}

function renderStaff(staffList) {
  staffContainer.innerHTML = "";

  if (staffList.length === 0) {
    showStatus("No staff match your search or filter.", "warning");
    return;
  }

  clearStatus();
  staffList.forEach((person) => {
    staffContainer.appendChild(createStaffCard(person));
  });
}

function openStaffModal(person) {
  modalName.textContent = person.name;
  modalBody.innerHTML = `
    <img src="${person.image}" alt="Photo of ${person.name}" />
    <p class="mb-1"><strong>Job Title:</strong> ${person.jobTitle}</p>
    <p class="mb-1"><strong>Research Area:</strong> ${person.researchArea}</p>
    <p class="mb-1"><strong>Email:</strong> ${person.email}</p>
    <p class="mb-1"><strong>Phone:</strong> ${person.phone}</p>
    <p class="mb-0"><strong>Location:</strong> ${person.location}</p>
  `;
  staffModal.show();
}

function populateAreaFilter(staffList) {
  const uniqueAreas = [...new Set(staffList.map((p) => p.researchArea))].sort();
  uniqueAreas.forEach((area) => {
    const option = document.createElement("option");
    option.value = area;
    option.textContent = area;
    areaFilter.appendChild(option);
  });
}

function applyFilters() {
  const searchTerm = searchInput.value.trim().toLowerCase();
  const selectedArea = areaFilter.value;

  const filtered = allStaff.filter((person) => {
    const matchesSearch =
      searchTerm === "" ||
      person.jobTitle.toLowerCase().includes(searchTerm) ||
      person.researchArea.toLowerCase().includes(searchTerm) ||
      person.name.toLowerCase().includes(searchTerm);

    const matchesArea =
      selectedArea === "" || person.researchArea === selectedArea;

    return matchesSearch && matchesArea;
  });

  renderStaff(filtered);
}

searchInput.addEventListener("input", applyFilters);
areaFilter.addEventListener("change", applyFilters);

function showStatus(message, type = "info") {
  statusMessage.innerHTML = `<div class="alert alert-${type}">${message}</div>`;
}

function clearStatus() {
  statusMessage.innerHTML = "";
}
