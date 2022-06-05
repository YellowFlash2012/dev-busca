
    let form = document.querySelector('.form'); let pageLinks =
    document.querySelectorAll('.page-link'); if (form){" "}
    {pageLinks.forEach((pageLink) => {
        pageLink.addEventListener("click", function (e) {
            e.preventDefault();
            console.log("Yeah, it works!");

            let page = this.dataset.page;

            form.innerHTML += `<input value=${page} name="page" />`;

            form.submit();
        });
    })}

