document.addEventListener('DOMContentLoaded', function () {
    // استرجاع وتفعيل التبويب الرئيسي
    var mainActiveTab = localStorage.getItem('mainActiveTab')
    if (mainActiveTab) {
        var mainTabElement = document.querySelector(`a[href="${mainActiveTab}"]`)
        if (mainTabElement) {
            mainTabElement.click()
        }
    }

    // استرجاع وتفعيل التبويب الفرعي (داخل sales)
    var salesActiveTab = localStorage.getItem('salesActiveTab')
    if (salesActiveTab) {
        var salesTabElement = document.querySelector(`a[href="${salesActiveTab}"]`)
        if (salesTabElement) {
            salesTabElement.click()
        }
    }

    // حفظ التبويب الرئيسي عند تغييره
    document.querySelectorAll('#myTab .nav-link').forEach(function (tab) {
        tab.addEventListener('click', function () {
            localStorage.setItem('mainActiveTab', this.getAttribute('href'))
        })
    })

    // حفظ التبويب الفرعي داخل Sales عند تغييره
    document.querySelectorAll('#salesTab .nav-link').forEach(function (tab) {
        tab.addEventListener('click', function () {
            localStorage.setItem('salesActiveTab', this.getAttribute('href'))
        })
    })
})