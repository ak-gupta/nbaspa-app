/**
 * @module Player career impact overview
 */

loadImpactProfile(
    PlayerID=PlayerID,
    result => {
        drawTimeChart(
            result,
            dateVar="YEAR",
            dateVarFormat="%Y",
            axisFormat="%Y",
            tag="#timeGraph"
        )
    }
)
