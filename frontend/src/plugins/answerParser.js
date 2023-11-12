function parsErrorAnswer(errorDetail) {
    let err = null

    if (Array.isArray(errorDetail)) {
        err = {}
        errorDetail.forEach(obj => {
            err[obj.loc.slice(-1)] = obj.msg
        })
        err = JSON.stringify(err)
    }

    else if (typeof errorDetail === 'object') {
        err = {}
        err[errorDetail.loc.slice(-1)] = errorDetail.msg
        err = JSON.stringify(err)
    }

    else {
        err = errorDetail
    }

    return err
}

export default parsErrorAnswer