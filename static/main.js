document.getElementById("getTokenBtn").addEventListener("click", async () => {
    const errorElement = document.getElementById("error");
    errorElement.classList.add("hidden");
    errorElement.textContent = "";

    try {
        const loginUrl = "https://login.dnevnik.ru/login/";
        const returnUrl = "https://login.dnevnik.ru/oauth2?response_type=token&client_id=bb97b3e445a340b9b9cab4b9ea0dbd6f&scope=CommonInfo,ContactInfo,FriendsAndRelatives,EducationalInfo";

        // Выполняем запрос через сервер, чтобы обойти CORS
        const response = await fetch("/proxy", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ loginUrl, returnUrl })
        });

        if (!response.ok) {
            throw new Error("Ошибка запроса к login.dnevnik.ru");
        }

        const data = await response.json();
        if (data.url) {
            // Отправляем URL на сервер для обработки
            const tokenResponse = await fetch("/get-token", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ url: data.url })
            });

            if (!tokenResponse.ok) {
                throw new Error("Ошибка получения токена");
            }

            // Перенаправляем на страницу результата
            window.location.href = "/get-token?url=" + encodeURIComponent(data.url);
        } else {
            throw new Error("URL не получен");
        }
    } catch (error) {
        errorElement.textContent = "Ошибка: " + error.message;
        errorElement.classList.remove("hidden");
    }
});