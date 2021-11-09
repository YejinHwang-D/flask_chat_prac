var invitation; // global variable
var connectionId_Faber;
var connectionId_Alice;

$(document).ready(() => {
    // 초대장 생성
    $("#btnCreate").click(() => {
        $.ajax({
            type: "POST",
            url: "http://127.0.0.1:5000/connections/create-invitation",
        })
            .done((response) => {
                invitation = response.invitation; // typeof() - object
                invitation = JSON.stringify(invitation); // make JSON

                connectionId_Faber = response.connection_id;

                console.log("Faber: " + connectionId_Faber);

                const appendedTag = `
                        <br>
                        <input type="button" id="btnSend" value="초대장 발송">
                    `;
                $("#formInvitation").append(appendedTag);
            })
    });

    // 초대장 발송
    $(document).on("click", "#btnSend", () => {
        $.ajax({
            type: "POST",
            url: "http://127.0.0.1:5000/connections/receive-invitation",
            data: invitation,
            datatype: "json"
        })
            .done((response) => {
                connectionId_Alice = response.connection_id;
                console.log("Alice: " + connectionId_Alice);
                
                const appendedTag = `
                    <br>
                    <input type="submit" id="btnDone" value="완료">
                    <input type="hidden" name="createConnection">
                    <input type="hidden" name="faberId" value="${connectionId_Faber}">
                    <input type="hidden" name="aliceId" value="${connectionId_Alice}">
                    `;
                $("#formInvitation").append(appendedTag);
            })
    });

    // 연결 끊기
    $(document).on("click", "#btnDeleteConnection", () => {
        $.ajax({
            type: "DELETE",
            url: `http://localhost:8021/connections/${connectionId_Faber}`,
            datatype: "json"
        })
            .done((response) => {
                console.log(response);
                console.log("Connection has been deleted")
            })
    });


    $(document).on("click", "#checkFaber", () => {
        $.ajax({
            type: "GET",
            url: `http://localhost:8021/connections/${connectionId_Faber}`,
        })
            .done((response) => {
                const appendedTag = `
                        <span>connected to ${response["their_label"]} (${response["their_role"]})</span>
                    `;
                $("#Faber").append(appendedTag);
            })
            .fail(() => { console.log("error"); })
    });

    $(document).on("click", "#checkAlice", () => {
        $.ajax({
            type: "GET",
            url: `http://localhost:8031/connections/${connectionId_Alice}`,
        })
            .done((response) => {
                const appendedTag = `
                        <span>connected to ${response["their_label"]} (${response["their_role"]})</span>
                    `;
                $("#Alice").append(appendedTag);
            })
            .fail(() => { console.log("error"); })
    });
})