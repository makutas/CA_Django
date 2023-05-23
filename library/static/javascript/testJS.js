function testJS() {
    var confirmation = confirm('Are you sure you want to delete this book instance?');

    if (confirmation) {
        return true;
    } else {
        return false;
    }
}