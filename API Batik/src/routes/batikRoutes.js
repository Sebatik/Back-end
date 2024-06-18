const express = require('express')
const router = express.Router()
const { getAllBatik, getAllBatikPosts } = require("../controllers/batikControllers")

router.route ("/all-posts").get(getAllBatikPosts)
router.route ("/all").get(getAllBatik)

module.exports = router