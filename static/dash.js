const roleSelect = document.querySelector('#role-select');
const categoryContainer = document.querySelector('.category-container');

roleSelect.addEventListener('change', function() {
    const activeRole = this.value;
    categoryContainer.innerHTML = '';
    const categories = Object.keys({{ privileges[activeRole]|tojson|safe }});

    categories.forEach(function(category) {
        const categoryPrivileges = {{ privileges[activeRole][category]|tojson|safe }};
        const categoryDiv = document.createElement('div');
        categoryDiv.classList.add('category');
        const categoryHeader = document.createElement('h3');
        categoryHeader.innerText = category;
        categoryDiv.appendChild(categoryHeader);
        const navList = document.createElement('ul');
        navList.classList.add('nav-list');

        categoryPrivileges.forEach(function(privilege) {
            const navItem = document.createElement('li');
            const navLink = document.createElement('a');
            navLink.href = '#';
            navLink.classList.add('nav-link');
            navLink.innerText = privilege;
            navItem.appendChild(navLink);
            navList.appendChild(navItem);
        });

        categoryDiv.appendChild(navList);
        categoryContainer.appendChild(categoryDiv);
    });
});
