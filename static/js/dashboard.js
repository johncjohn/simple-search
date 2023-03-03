$(document).ready(function() {
    // Get the select element for the roles
    const roleSelect = document.getElementById("role-select");

    // Get the privileges for each role
    const privileges = JSON.parse('{{ privileges | tojson }}');

    // Function to update the navigation list with the privileges of the selected role
    const updateNavList = () => {
        // Get the active role
        const activeRole = roleSelect.value;

        // Get the container for the navigation list
        const navListContainer = document.getElementById("nav-list-container");

        // Clear the container
        navListContainer.innerHTML = "";

        // Loop through the categories for the active role
        for (const category in privileges[activeRole]) {
            // Create a container for the category
            const categoryContainer = document.createElement("div");
            categoryContainer.className = "nav-list-container";

            // Create a header for the category
            const categoryHeader = document.createElement("h2");
            categoryHeader.textContent = category;
            categoryContainer.appendChild(categoryHeader);

            // Create a list for the privileges in the category
            const categoryList = document.createElement("ul");
            categoryList.className = "nav-list";

            // Loop through the privileges in the category
            for (const privilege of privileges[activeRole][category]) {
                // Create a list item for the privilege
                const privilegeItem = document.createElement("li");

                // Create a link for the privilege
                const privilegeLink = document.createElement("a");
                privilegeLink.href = privilege.url;
                privilegeLink.textContent = privilege.name;
                privilegeLink.className = "nav-link";

                // Add the link to the list item and the list item to the list
                privilegeItem.appendChild(privilegeLink);
                categoryList.appendChild(privilegeItem);
            }

            // Add the list to the category container
            categoryContainer.appendChild(categoryList);

            // Add the category container to the navigation list container
            navListContainer.appendChild(categoryContainer);
        }
    };

    // Attach the updateNavList function to the change event of the role select
    roleSelect.addEventListener("change", updateNavList);

    // Call the updateNavList function to initialize the navigation list
    updateNavList();
  });
    

