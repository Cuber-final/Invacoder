// 代码块功能依赖

$(function () {
    $('pre').wrap('<div class="code-area" style="position: relative "></div>');
});

//使用layer自带图片放大功能
$(document).ready(function () {
    var content = '<div class="img-scale"></div>'
    $('.article-body img').wrap(content)
    $('.article-body img').each(function () {
        // 使用each函数可遍历对象逐个添加
        var getSrc = $(this).attr("src")
        $(this).attr("layer-src", getSrc)
    })
});

$(function () {
    layer.photos({
        photos: '.img-scale', //选取图片所在容器
        anim: 5 //0-6的选择，指定弹出图片动画类型，默认随机（请注意，3.0之前的版本用shift参数）
    });
})

// 代码块一键复制
$(function () {
    var $copyIcon = $('<i class="iconfont copyBtn" title="复制代码" aria-hidden="true">&#xe6ea;</i>')
    // var $notice = $('<div class="codecopy_notice"></div>')
    $('.code-area').prepend($copyIcon)
    // $('.code-area').prepend($notice)
    // “复制成功”字出现
    function copy(text, ctx) {
        if (document.queryCommandSupported && document.queryCommandSupported('copy')) {
            try {
                document.execCommand('copy')
                // 此命令以逐渐被弃用，有无新的兼容方式
                layer.msg("复制成功")

            } catch (ex) {
                layer.msg("复制失败")
                return false
            }
        } else {
            layer.msg("不支持复制")
        }
    }

    // 复制
    $('.copyBtn').on('click', function () {
        var selection = window.getSelection()
        var range = document.createRange()
        range.selectNodeContents($(this).siblings('pre').find('code')[0])
        selection.removeAllRanges()
        selection.addRange(range)
        var text = selection.toString()
        var filtered = text.replace(/<\/?.+?>/g, "")
        // remove HTML tag
        copy(filtered, this)
        // copy(text, this)
        selection.removeAllRanges()
        // 去掉聚焦粘贴板效果
    })
});