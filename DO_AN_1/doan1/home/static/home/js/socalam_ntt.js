document.addEventListener('DOMContentLoaded', () => {
    // Hiển thị form ca làm
    const btnntt = document.getElementById('tcl');
    const btndong = document.getElementById('dong');
    const form = document.getElementById('form_calam_ntt');
    let form_open = false;

    btnntt.addEventListener('click', () => {
        form_open = !form_open;
        form.style.display = form_open ? 'block' : 'none';
    });

    btndong.addEventListener('click', () => {
        form.style.display = 'none';
        form_open = false;
    });

    // Overlay xóa ca làm
    const overlay = document.createElement('div');
    overlay.className = 'overlay';
    document.body.appendChild(overlay);

    const deleteButtons = document.querySelectorAll('.nut-xoa');
    const cancelButtons = document.querySelectorAll('.nut-huy');

    deleteButtons.forEach(button => {
        button.addEventListener('click', function () {
            const id = this.getAttribute('data-id');
            const form = document.getElementById(`form-xoa-${id}`);

            document.querySelectorAll('.xoa-form').forEach(f => {
                f.style.display = f === form ? 'block' : 'none';
            });

            overlay.style.display = 'block';
        });
    });

    cancelButtons.forEach(button => {
        button.addEventListener('click', function () {
            const id = this.getAttribute('data-id');
            const form = document.getElementById(`form-xoa-${id}`);
            form.style.display = 'none';
            overlay.style.display = 'none';
        });
    });

    overlay.addEventListener('click', function () {
        document.querySelectorAll('.xoa-form').forEach(form => {
            form.style.display = 'none';
        });
        overlay.style.display = 'none';
    });

    // Import ca làm
    const btnimport = document.getElementById('import');
    const btndongimport = document.getElementById('dongimport');
    const form_import = document.getElementById('form_import_calam');
    let form_import_open = false;

    btnimport.addEventListener('click', () => {
        form_import_open = !form_import_open;
        form_import.style.display = form_import_open ? 'block' : 'none';
    });

    btndongimport.addEventListener('click', () => {
        form_import.style.display = 'none';
        form_import_open = false;
    });

    // Sửa ca làm
    const nutSua = document.querySelectorAll('.sua');
    const popup = document.getElementById('form_calam_sua');
    const closeBtn = document.querySelector('.dongsua');

    nutSua.forEach(button => {
        button.addEventListener('click', function () {
            const macalam = this.getAttribute('data-id');
            const ngay = this.getAttribute('data-ngay') 
                ? new Date(this.getAttribute('data-ngay')).toISOString().split('T')[0] 
                : '';
            const giobd = this.getAttribute('data-giobd');
            const giokt = this.getAttribute('data-giokt');

            document.getElementById('macalam').value = macalam;
            document.getElementById('ngay').value = ngay;
            document.getElementById('giobd').value = giobd;
            document.getElementById('giokt').value = giokt;

            const form = document.getElementById('form_sua');
            form.action = `/sua_calam/${macalam}/`;
            popup.style.display = 'block';
        });
    });

    closeBtn.addEventListener('click', function () {
        popup.style.display = 'none';
    });

    window.addEventListener('click', function (e) {
        if (e.target == popup) {
            popup.style.display = 'none';
        }
    });

    // Lọc bảng theo ngày
    const filterBtn = document.querySelector('.loc-nut');
    const dateFilter = document.querySelector('.date-filter');
    const startDate = document.getElementById('ngaybatdau');
    const endDate = document.getElementById('ngayketthuc');
    const tableRows = document.querySelectorAll('#maintenanceTableBody tr[data-date]');

    filterBtn.addEventListener('click', function (e) {
        e.stopPropagation();
        dateFilter.classList.toggle('show');
    });

    document.addEventListener('click', function (e) {
        if (!dateFilter.contains(e.target) && !filterBtn.contains(e.target)) {
            dateFilter.classList.remove('show');
        }
    });

    dateFilter.addEventListener('click', function (e) {
        e.stopPropagation();
    });

    function filterTable() {
        const start = startDate.value;
        const end = endDate.value;

        if (!start || !end) return;

        tableRows.forEach(row => {
            const rowDate = row.getAttribute('data-date');
            row.style.display = (rowDate >= start && rowDate <= end) ? '' : 'none';
        });

        filterBtn.innerHTML = `Từ ${start} đến ${end} <i class="ti-angle-down"></i>`;
    }

    startDate.addEventListener('change', filterTable);
    endDate.addEventListener('change', filterTable);
});