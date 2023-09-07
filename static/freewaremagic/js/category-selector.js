 // Define a JavaScript object to store subcategories for each category
  const subcategories = {
    "Browsers": ["Add-ons & Tools", "Web browsers"],
    "Business & Productivity": ["CategoryA", "CategoryB"], // Add subcategories for other categories
    "Games": ["Action", "Adventure", "Arcade", "Board", "Card", "Casino", "Educational", "Family", "Music", "Puzzle", "Racing", "Role Playing", "Simulation", "Sports", "Strategy", "Trivia", "Utilities", "Word"]
  };

  // Function to populate the subcategory dropdown based on the selected category
  function populateSubcategories() {
    const categorySelect = document.getElementById("categorySelect");
    const subcategorySelect = document.getElementById("subcategorySelect");
    const selectedCategory = categorySelect.value;

    // Clear existing options in subcategory dropdown
    subcategorySelect.innerHTML = "";

    // Populate subcategory dropdown with options from the selected category
    const categorySubcategories = subcategories[selectedCategory] || [];
    categorySubcategories.forEach(subcategory => {
      const option = document.createElement("option");
      option.text = subcategory;
      subcategorySelect.add(option);
    });
  }

  // Add an event listener to the category dropdown to trigger subcategory population
  const categorySelect = document.getElementById("categorySelect");
  categorySelect.addEventListener("change", populateSubcategories);

  // Initial population of subcategories based on the default category selection
  populateSubcategories();